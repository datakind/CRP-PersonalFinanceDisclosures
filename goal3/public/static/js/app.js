
var search = instantsearch({
  // Replace with your own values
  appId: 'MMO9C5ZZD6',
  apiKey: '521bc2336afc51528bd5a058bc7aefe2', // search only API key, no ADMIN key
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
