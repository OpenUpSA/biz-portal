import { MDCTopAppBar } from "@material/top-app-bar";
import { MDCDrawer } from "@material/drawer";

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
      return response.results.map(({ registered_name }) => ({
        value: registered_name
      }));
    }
  }
});

// Instantiate the Typeahead UI
$("#custom-templates .typeahead").typeahead(null, {
  name: "businesses",
  displayKey: "value",
  source: businesses,
  async: false,
  templates: {
    empty: [
      '<div class="empty-message">',
      "unable to find the business you are looking for",
      "</div>"
    ].join("\n"),
    suggestion: data => {
      console.log(333, data);
      return `<a class="search-result-links" href="/portal-test/${data.value}"><p class="text-menu-search">${data.value}</p></a>`;
    }
  }
});
