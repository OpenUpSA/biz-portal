import {MDCDialog} from '@material/dialog';
const dialog = new MDCDialog(document.querySelector('.mdc-dialog'));

const openProfileModal = document.querySelector('#show').addEventListener('click', () => {
    dialog.open();
  })

export default openProfileModal;
