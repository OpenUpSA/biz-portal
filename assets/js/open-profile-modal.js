import {MDCDialog} from '@material/dialog';

const dialogNode = document.querySelector('.mdc-dialog');
let openProfileModal;

if (!!dialogNode) {
  const dialog = new MDCDialog(dialogNode);

  openProfileModal = document.querySelector('#show-business-menu').addEventListener('click', () => {
    dialog.open();
  })

}

export default openProfileModal;
