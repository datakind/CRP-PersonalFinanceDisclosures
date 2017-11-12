var client = algoliasearch("APPID", "APPKEY")
var master_disclosure = client.initIndex('master_disclosure');
var bills = client.initIndex('bills');
var members = client.initIndex('members');
var candidates = client.initIndex('candidates');
var committees = client.initIndex('committees');

autocomplete('#search-input', {}, [
    {
      source: autocomplete.sources.hits(candidates, { hitsPerPage: 3 }),
      displayKey: 'CRPName',
      templates: {
        header: '<div class="aa-suggestions-category">Candidates</div>',
        suggestion: function(suggestion) {
          return '<span>' + suggestion._highlightResult.CRPName.value + '</span>';
        }
      }
    },
    {
      source: autocomplete.sources.hits(master_disclosure, { hitsPerPage: 3 }),
      displayKey: 'Orgname',
      templates: {
        header: '<div class="aa-suggestions-category">Disclosures</div>',
        suggestion: function(suggestion) {
          return '<span>' +
            suggestion._highlightResult.Orgname.value + '</span><span> 20'
              + suggestion._highlightResult.CalendarYear.value + '</span>';
        }
      }
    }
    ,
    {
      source: autocomplete.sources.hits(bills, { hitsPerPage: 3 }),
      displayKey: 'official_title',
      templates: {
        header: '<div class="aa-suggestions-category">Bills</div>',
        suggestion: function(suggestion) {
          return '<span>' +
            suggestion._highlightResult.official_title.value +'</span><span>'+ ' BillID: ' + suggestion._highlightResult.bill_id.value+'</span>';
        }
      }
    }
]);