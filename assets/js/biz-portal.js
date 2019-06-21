import {MDCTopAppBar} from "@material/top-app-bar";
import {MDCDrawer} from "@material/drawer";
import {MDCTextField} from '@material/textfield';
import {MDCTextFieldIcon} from '@material/textfield/icon';

// Instantiate MDC Drawer
const drawerEl = document.querySelector('.mdc-drawer');
const drawer = new MDCDrawer(drawerEl);

// Instantiate MDC TopAppBar
const topAppBar = MDCTopAppBar.attachTo(document.getElementById('app-bar'));
topAppBar.setScrollTarget(document.getElementById('main-content'));
topAppBar.listen('MDCTopAppBar:nav', () => {
  drawer.open = !drawer.open;
});

// Instantiate MDC TextField
MDCTextField.attachTo(document.querySelector('.mdc-text-field'));
MDCTextFieldIcon.attachTo(document.querySelector('.mdc-text-field-icon'));
