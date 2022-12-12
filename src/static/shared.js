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
