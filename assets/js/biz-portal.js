require('corejs-typeahead/dist/typeahead.jquery');
const Bloodhound = require('corejs-typeahead/dist/bloodhound');

import {MDCTopAppBar} from "@material/top-app-bar";
import {MDCDrawer} from "@material/drawer";

// Instantiate MDC Drawer
const drawerEl = document.querySelector(".mdc-drawer");
const drawer = new MDCDrawer(drawerEl);

// Instantiate MDC TopAppBar
const topAppBar = MDCTopAppBar.attachTo(document.getElementById("app-bar"));
topAppBar.setScrollTarget(document.getElementById("main-content"));
topAppBar.listen("MDCTopAppBar:nav", () => {
  drawer.open = !drawer.open;
});

// Instantiate the Bloodhound suggestion engine
var businesses = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.obj.whitespace("value"),
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: {
    wildcard: "%QUERY",
    url: `/api/v1/businesses/?search=%QUERY`,
    transform: response => {
      return response.results;
    }
  }
});

// Instantiate the Typeahead UI
$("#custom-templates .typeahead").typeahead(null, {
  name: "businesses",
  displayKey: "registered_name",
  source: businesses,
  templates: {
    empty: [
      '<div class="empty-message">',
      "Business not found",
      "</div>"
    ].join("\n"),
    footer : (context) => (
      `<a class="search-result-links" href="/businesses/?q=${context.query}"><p class="more-results-search">More results</p></a>`),
    suggestion: data => {
      const { web_url, registered_name } = data;
      return `<a class="search-result-links" href="${web_url}"><p class="text-menu-search">${registered_name}</p></a>`;
    }
  }
});
