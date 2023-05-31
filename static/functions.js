function filterTable() {
  var checkboxes = document.querySelectorAll('#checkboxContainer input[type="checkbox"]');
  var table = document.getElementById("myTable");
  var rows = table.getElementsByTagName("tr");

  for (var i = 1; i < rows.length; i++) {
    var dayCell = rows[i].getElementsByTagName("td")[3];
    var day = dayCell.textContent || dayCell.innerText;
    var shouldShow = false;

    for (var j = 0; j < checkboxes.length; j++) {
      if (checkboxes[j].checked && checkboxes[j].value === day) {
        shouldShow = true;
        break;
      }
    }
 
    rows[i].style.display = shouldShow ? "" : "none";
  }
}

function updateMessagePreview() {
  var date = document.getElementById("dateInput").value;
  var time = document.getElementById("timeInput").value;
  var availabilityLength = document.getElementById("availabilityInput").value;

  var messagePreview = "Hello, I am contacting everyone on my waitlist as " + availabilityLength + " minute slot available on " + date + " starting on " + time;
  document.getElementById("messagePreview").value = messagePreview;
}

// Attach event listeners to update preview on field changes
document.getElementById("dateInput").addEventListener("change", updateMessagePreview);
document.getElementById("timeInput").addEventListener("change", updateMessagePreview);
document.getElementById("availabilityInput").addEventListener("input", updateMessagePreview);