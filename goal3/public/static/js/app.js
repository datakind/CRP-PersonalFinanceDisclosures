
var search = instantsearch({
  // Replace with your own values
  appId: 'APPID',
  apiKey: 'APPKEY', // search only API key, no ADMIN key
  indexName: 'master_disclosure',
  urlSync: true
});

search.addWidget(
  instantsearch.widgets.stats({
    container: '#stats'
  })
);


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
