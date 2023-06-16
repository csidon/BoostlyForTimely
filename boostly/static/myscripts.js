// Call the function on page load
//window.addEventListener('load', hideNavbar);

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

function hideNavbar() {
  // Get the current URL
  var currentUrl = window.location.href;

  // List of URLs where the navbar should be hidden
  var pagesToHideNavbar = [
    '/home',
    'login',
    '/register'
  ];

  // Check if the current URL matches any of the pages in the list
  if (pagesToHideNavbar.some(function(pageUrl) {
    return currentUrl.endsWith(pageUrl);
  })) {
    // The navbar should be hidden
    var navbar = document.getElementById('navbarToHide');
    if (navbar) {
      navbar.style.display = 'none';
    }
  }
}

import { Grid, h, html } from "https://unpkg.com/gridjs?module";


//function createDropdownButton(cell, row, rowIndex) {
//    const clientID = rowIndex + 1;
//    alert("it reads js");
//    return h('div', {}, [
//        h('div', {
//            className: 'btn-group',
//        }, [
//            h('button', {
//                className: 'btn btn-success btn-sm rounded-0 fa fa-edit dropdown-toggle',
//                type: 'button',
//                'data-toggle': 'dropdown',
//                'aria-haspopup': 'true',
//                'aria-expanded': 'false',
//            }),
//            h('div', {
//                className: 'dropdown-menu',
//            }, [
//                h('a', {
//                    className: 'dropdown-item',
//                    href: `/clientpref/${clientID}/update`,
//                }, 'Update client details'),
//            ]),
//        ]),
//    ]);
//}
//
//new Grid({
//    columns: [
//        { id: 'name', name: 'Name' },
//                  { id: 'minDuration', name: html('Min<br/>slot') },
//				{ id: 'mon', name: 'Mon', sort: true },
//				{ id: 'tue', name: 'Tues', sort: true },
//				{ id: 'wed', name: 'Wed', sort: true },
//				{ id: 'thur', name: 'Thur', sort: true },
//				{ id: 'fri', name: 'Fri', sort: true },
//				{ id: 'sat', name: 'Sat', sort: true },
//				{ id: 'sun', name: 'Sun', sort: true },
//				{ id: 'clientid', name: 'id', hidden: true},
//        { id: 'edit', name: '', formatter: createDropdownButton },
//        { id: 'delete', name: '', formatter: (cell, row) => {
//            return h('button', {
//                className: 'btn btn-danger btn-sm rounded-0 fa fa-trash',
//                onClick: () => alert(`Editing "${row.cells[0].data}" "${row.cells[1].data}" with id "${row.cells[5].data}"`)
//            }, '');
//        }},
//    ],
//    data: [
//        {% for client in clients %}
//				{
//					name: '{{ client.firstName }}' + ' ' + '{{ client.lastName}}',
//					minDuration:'{{ client.clientprefs.minDuration }}',
//					mon: '{{ Mon[client] }}',
//					tue: '{{ Tue[client] }}',
//					wed: '{{ Wed[client] }}',
//					thur: '{{ Thur[client] }}',
//					fri: '{{ Fri[client] }}',
//					sat: '{{ Sat[client] }}',
//					sun: '{{ Sun[client] }}',
//
//					email: '{{ client.email }}',
//					  mobile: '{{ client.mobile }}',
//					  status: '{{ client.status }}',
//					  clientid: '{{ client.id }}',
//
//				},
//		{% endfor %}
//    ],
//    search: {
//			  selector: (cell, rowIndex, cellIndex) => [0, 1, 4].includes(cellIndex) ? cell : null,
//			},
//			sort: true,
//			pagination: true,
//}).render(document.getElementById('table'));

