const { dbQuery } = require('../src/database');

async function testMissingAwait() {
  console.log('Testing operation WITHOUT await:');
  // OMITTING await on Promise returned by dbQuery.get
  const resultPromise = dbQuery.get('SELECT * FROM books WHERE id = 1');
  console.log('Result variable value (missing await):', resultPromise);
  console.log('Accessing title directly:', resultPromise.title); // undefined because it is a Promise!

  console.log('\nTesting operation WITH await:');
  const actualResult = await dbQuery.get('SELECT * FROM books WHERE id = 1');
  console.log('Result variable value (with await):', actualResult);
  console.log('Accessing title correctly:', actualResult.title);

  process.exit(0);
}

testMissingAwait();
