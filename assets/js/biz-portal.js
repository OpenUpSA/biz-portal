import {MDCTopAppBar} from "@material/top-app-bar";
import {MDCDrawer} from "@material/drawer";

// Instantiate MDC Drawer
const drawerEl = document.querySelector('.mdc-drawer');
const drawer = new MDCDrawer(drawerEl);

// Instantiate MDC TopAppBar
const topAppBar = MDCTopAppBar.attachTo(document.getElementById('app-bar'));
topAppBar.setScrollTarget(document.getElementById('main-content'));
topAppBar.listen('MDCTopAppBar:nav', () => {
  drawer.open = !drawer.open;
});


// Instantiate the Bloodhound suggestion engine
var businesses = new Bloodhound({
datumTokenizer: function (datum) {
    return Bloodhound.tokenizers.whitespace(datum.value);
},
queryTokenizer: Bloodhound.tokenizers.whitespace,
remote: {
    wildcard: '%QUERY',
    url: `/api/v1/businesses/?search=%QUERY`,
    filter: function (businesses) {
        // Map the remote source JSON array to a JavaScript object array
        return $.map(businesses.results, function (business) {
            return {
                value: business.registered_name
            };
        });
    }
  }
});

// Initialize the Bloodhound suggestion engine
businesses.initialize();

// Instantiate the Typeahead UI

const suggestions = $('#custom-templates .typeahead').typeahead(null, {
  name: 'matched-links',
  displayKey: 'value',
  source: businesses.ttAdapter(),
  templates: {
    empty: [
      '<div class="empty-message">',
      'unable to find the business you are looking for',
      '</div>'
    ].join('\n'),
      suggestion: function(data) {
        return `<a class="search-result-links" href="/portal-test/${data.value}"><p class="text-menu-search">${data.value}</p></a>`;
    }
  }
});

