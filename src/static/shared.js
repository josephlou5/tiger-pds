function showHidePinNumber(pinElement, buttonElement) {
  buttonElement.click((event) => {
    pinElement.toggleClass('d-none');
    if (buttonElement.html().trim() === 'Show') {
      buttonElement.html('Hide');
    } else {
      buttonElement.html('Show');
    }
  });
}

function ajaxRequest(method, url, { success, error } = {}) {
  if (!success) {
    success = () => {
      location.reload();
    };
  }
  if (!error) {
    error = (res) => {
      alert(res.responseText);
      location.reload();
    };
  }
  $.ajax({ method, url, success, error });
}
