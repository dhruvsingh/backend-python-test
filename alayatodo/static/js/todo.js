$("#todo_delete, #todo_complete").click(function(e) {
  e.preventDefault();

  var form = $("#todo_form");

  form.prop("action", $(this).data("url"));
  form.submit();
});