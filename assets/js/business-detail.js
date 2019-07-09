import {MDCDialog} from '@material/dialog';
const dialog = new MDCDialog(document.querySelector('.mdc-dialog'));

const businessProfileModal = document.querySelector('#show').addEventListener('click', () => {
  
    dialog.open();
      
  })

export default businessProfileModal;
