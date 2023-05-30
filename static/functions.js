function filterTable() {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    var table = document.getElementById("myTable");
    var rows = table.getElementsByTagName("tr");

    for (var i = 1; i < rows.length; i++) {
      var dayCell = rows[i].getElementsByTagName("td")[0];
      var day = dayCell.textContent || dayCell.innerText;
      var shouldShow = false;

      for (var j = 0; j < checkboxes.length; j++) {
        if (checkboxes[j].checked && checkboxes[j].id === "checkbox" + day) {
          shouldShow = true;
          break;
        }
      }

      rows[i].style.display = shouldShow ? "" : "none";
    }
  }