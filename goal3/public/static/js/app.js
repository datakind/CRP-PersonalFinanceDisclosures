
var search = instantsearch({
  // Replace with your own values
  appId: 'APPID',
  apiKey: 'APIKEY', // search only API key, no ADMIN key
  indexName: 'master_disclosure',
  urlSync: true
});

search.addWidget(
  instantsearch.widgets.searchBox({
    container: '#search-input'
  })
);

function searchValue() {
  return document.getElementById('search-input').value;
}

search.addWidget(
  instantsearch.widgets.hits({
    container: '#hits',
    hitsPerPage: 10,
    templates: {
      item: document.getElementById('hit-template').innerHTML,
      empty: "We didn't find any results for the search <em>\"{{query}}\"</em>"
    }
  })
);

search.addWidget(
  instantsearch.widgets.pagination({
    container: '#pagination'
  })
);

search.start();

// var client = algoliasearch('APP_ID', 'APP_KEY');
// var index = client.initIndex('master_disclosure');

// // perform query "jim"
// index.search('N00029391', searchCallback);

// // the last optional argument can be used to add search parameters
// index.search(
//   'N00029391', {
//     hitsPerPage: 5,
//     facets: '*',
//     maxValuesPerFacet: 10
//   },
//   searchCallback
// );

// function searchCallback(err, content) {
//   if (err) {
//     console.error(err);
//     return;
//   }

//   console.log(content);
// }