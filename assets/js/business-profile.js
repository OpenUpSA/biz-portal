import {MDCRipple} from '@material/ripple';

let buttonRipple;

if (!!document.querySelector('.mdc-button')) {
  buttonRipple = new MDCRipple(document.querySelector('.mdc-button'));
}

export default buttonRipple;
