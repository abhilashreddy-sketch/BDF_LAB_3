const http = require('http');
const app = require('../src/app');
const { initializeDatabase, seedSampleData } = require('../src/database');

const TEST_PORT = 3055;
let server;

function makeRequest(method, path, body = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'localhost',
      port: TEST_PORT,
      path: path,
      method: method,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => {
        data += chunk;
      });
      res.on('end', () => {
        let json = null;
        try {
          json = JSON.parse(data);
        } catch (e) {
          json = data;
        }
        resolve({
          status: res.statusCode,
          headers: res.headers,
          data: json
        });
      });
    });

    req.on('error', (e) => reject(e));

    if (body) {
      req.write(JSON.stringify(body));
    }
    req.end();
  });
}

const testCases = [
  {
    id: 'TC-01',
    scenario: 'GET all books (initial fetch)',
    method: 'GET',
    path: '/books',
    body: null,
    expectedStatus: 200,
    check: (res) => res.data.message === 'Books retrieved successfully' && Array.isArray(res.data.data)
  },
  {
    id: 'TC-02',
    scenario: 'GET existing book by ID',
    method: 'GET',
    path: '/books/1',
    body: null,
    expectedStatus: 200,
    check: (res) => res.data.data && res.data.data.id === 1
  },
  {
    id: 'TC-03',
    scenario: 'GET non-existent book by ID',
    method: 'GET',
    path: '/books/9999',
    body: null,
    expectedStatus: 404,
    check: (res) => res.data.message === 'Book not found'
  },
  {
    id: 'TC-04',
    scenario: 'POST valid book creation',
    method: 'POST',
    path: '/books',
    body: { title: 'Mastering TypeScript', author: 'Boris Cherny', price: 550 },
    expectedStatus: 201,
    check: (res) => res.data.message === 'Book created successfully' && res.data.data.title === 'Mastering TypeScript'
  },
  {
    id: 'TC-05',
    scenario: 'POST missing title validation',
    method: 'POST',
    path: '/books',
    body: { author: 'Boris Cherny', price: 550 },
    expectedStatus: 400,
    check: (res) => res.data.message === 'Title, author and valid numeric price are required'
  },
  {
    id: 'TC-06',
    scenario: 'POST missing author validation',
    method: 'POST',
    path: '/books',
    body: { title: 'Mastering TypeScript', price: 550 },
    expectedStatus: 400,
    check: (res) => res.data.message === 'Title, author and valid numeric price are required'
  },
  {
    id: 'TC-07',
    scenario: 'POST non-numeric price validation',
    method: 'POST',
    path: '/books',
    body: { title: 'Mastering TypeScript', author: 'Boris Cherny', price: 'free' },
    expectedStatus: 400,
    check: (res) => res.data.message === 'Title, author and valid numeric price are required'
  },
  {
    id: 'TC-08',
    scenario: 'PUT update existing book',
    method: 'PUT',
    path: '/books/1',
    body: { title: 'Python Programming - Second Edition', author: 'John Smith', price: 499 },
    expectedStatus: 200,
    check: (res) => res.data.message === 'Book updated successfully' && res.data.data.price === 499
  },
  {
    id: 'TC-09',
    scenario: 'PUT non-existent book',
    method: 'PUT',
    path: '/books/9999',
    body: { title: 'Ghost Book', author: 'Anonymous', price: 100 },
    expectedStatus: 404,
    check: (res) => res.data.message === 'Book not found'
  },
  {
    id: 'TC-10',
    scenario: 'DELETE existing book',
    method: 'DELETE',
    path: '/books/2',
    body: null,
    expectedStatus: 200,
    check: (res) => res.data.message === 'Book deleted successfully' && res.data.data.id === 2
  },
  {
    id: 'TC-11',
    scenario: 'DELETE non-existent book',
    method: 'DELETE',
    path: '/books/9999',
    body: null,
    expectedStatus: 404,
    check: (res) => res.data.message === 'Book not found'
  },
  {
    id: 'TC-12',
    scenario: 'Search books by title using search_q',
    method: 'GET',
    path: '/books?search_q=Clean',
    body: null,
    expectedStatus: 200,
    check: (res) => res.data.data.some((b) => b.title.includes('Clean'))
  },
  {
    id: 'TC-13',
    scenario: 'Sort books ascending using order_by and order',
    method: 'GET',
    path: '/books?order_by=price&order=ASC',
    body: null,
    expectedStatus: 200,
    check: (res) => res.data.data[0].price <= res.data.data[res.data.data.length - 1].price
  },
  {
    id: 'TC-14',
    scenario: 'Sort books descending using order_by and order',
    method: 'GET',
    path: '/books?order_by=price&order=DESC',
    body: null,
    expectedStatus: 200,
    check: (res) => res.data.data[0].price >= res.data.data[res.data.data.length - 1].price
  },
  {
    id: 'TC-15',
    scenario: 'Pagination with limit and offset',
    method: 'GET',
    path: '/books?limit=3&offset=0',
    body: null,
    expectedStatus: 200,
    check: (res) => res.data.data.length === 3
  },
  {
    id: 'TC-16',
    scenario: 'Filter books by minimum price (min_price)',
    method: 'GET',
    path: '/books?min_price=500',
    body: null,
    expectedStatus: 200,
    check: (res) => res.data.data.every((b) => b.price >= 500)
  },
  {
    id: 'TC-17',
    scenario: 'Filter books by maximum price (max_price)',
    method: 'GET',
    path: '/books?max_price=400',
    body: null,
    expectedStatus: 200,
    check: (res) => res.data.data.every((b) => b.price <= 400)
  },
  {
    id: 'TC-18',
    scenario: 'Combined price range filter (min_price and max_price)',
    method: 'GET',
    path: '/books?min_price=300&max_price=600',
    body: null,
    expectedStatus: 200,
    check: (res) => res.data.data.every((b) => b.price >= 300 && b.price <= 600)
  },
  {
    id: 'TC-19',
    scenario: 'Combined search, sort, and pagination',
    method: 'GET',
    path: '/books?search_q=Design&order_by=price&order=ASC&limit=5&offset=0',
    body: null,
    expectedStatus: 200,
    check: (res) => res.data.data.length > 0 && res.data.data.every((b) => b.title.includes('Design'))
  },
  {
    id: 'TC-20',
    scenario: 'Invalid sorting parameter validation',
    method: 'GET',
    path: '/books?order_by=malicious_column',
    body: null,
    expectedStatus: 400,
    check: (res) => res.data.message.includes('Invalid order_by')
  },
  {
    id: 'TC-21',
    scenario: 'Invalid pagination limit value validation',
    method: 'GET',
    path: '/books?limit=-5',
    body: null,
    expectedStatus: 400,
    check: (res) => res.data.message.includes('Invalid limit')
  }
];

async function runTests() {
  console.log('Initializing database for automated API testing...');
  await initializeDatabase();
  await seedSampleData();

  server = app.listen(TEST_PORT, async () => {
    console.log(`Test server active on port ${TEST_PORT}\n`);
    console.log('========================================================================================');
    console.log('Test ID | Scenario                                            | Exp | Act | Status');
    console.log('========================================================================================');

    let passed = 0;
    let failed = 0;
    const testResults = [];

    for (const tc of testCases) {
      try {
        const res = await makeRequest(tc.method, tc.path, tc.body);
        const statusMatch = res.status === tc.expectedStatus;
        const logicMatch = tc.check ? tc.check(res) : true;
        const isPass = statusMatch && logicMatch;

        if (isPass) {
          passed++;
        } else {
          failed++;
        }

        const paddedId = tc.id.padEnd(7);
        const paddedScen = tc.scenario.padEnd(51);
        const statusStr = isPass ? 'PASS' : 'FAIL';
        console.log(`${paddedId} | ${paddedScen} | ${tc.expectedStatus} | ${res.status} | ${statusStr}`);

        testResults.push({
          id: tc.id,
          scenario: tc.scenario,
          method: tc.method,
          path: tc.path,
          expectedStatus: tc.expectedStatus,
          actualStatus: res.status,
          response: res.data,
          status: statusStr
        });
      } catch (err) {
        failed++;
        console.log(`${tc.id.padEnd(7)} | ${tc.scenario.padEnd(51)} | ${tc.expectedStatus} | ERR | FAIL (${err.message})`);
        testResults.push({
          id: tc.id,
          scenario: tc.scenario,
          method: tc.method,
          path: tc.path,
          expectedStatus: tc.expectedStatus,
          actualStatus: 'ERR',
          response: { error: err.message },
          status: 'FAIL'
        });
      }
    }

    console.log('========================================================================================');
    console.log(`Execution Summary: Total: ${testCases.length} | Passed: ${passed} | Failed: ${failed}`);
    console.log('========================================================================================\n');

    // Save test results to JSON file for report generation and audit
    const fs = require('fs');
    const path = require('path');
    fs.writeFileSync(
      path.resolve(__dirname, 'test_results.json'),
      JSON.stringify(testResults, null, 2)
    );

    server.close(() => {
      console.log('Test server closed.');
      process.exit(failed > 0 ? 1 : 0);
    });
  });
}

runTests();
