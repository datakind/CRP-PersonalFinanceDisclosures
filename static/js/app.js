var client = algoliasearch('APP_ID', 'APP_KEY');
var index = client.initIndex('master_disclosure');

// perform query "jim"
index.search('N00029391', searchCallback);

// the last optional argument can be used to add search parameters
index.search(
  'N00029391', {
    hitsPerPage: 5,
    facets: '*',
    maxValuesPerFacet: 10
  },
  searchCallback
);

function searchCallback(err, content) {
  if (err) {
    console.error(err);
    return;
  }

  console.log(content);
}