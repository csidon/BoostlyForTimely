function revealFunction(id, btn) {
  var todo = document.getElementById("todo-section");
  var progress = document.getElementById("progress-section");
  var done = document.getElementById("done-section");
  var overdue = document.getElementById("overdue-section");
  var archived = document.getElementById("archived-section");

//  const button1 = document.getElementById('todo-btn');
//  const button2 = document.getElementById('doing-btn');
//  const button3 = document.getElementById('done-btn');
//  const button4 = document.getElementById('overdue-btn');

    document.getElementById(id).style.display = 'block';
    // hide the lorem ipsum text
    if (btn == "todo"){
        progress.style.display = 'none';
        done.style.display = 'none';
        overdue.style.display = 'none';
        archived.style.display = 'none';
    }
    else if (btn == "done"){
        progress.style.display = 'none';
        todo.style.display = 'none';
        overdue.style.display = 'none';
        archived.style.display = 'none';
    }
    else if (btn == "progress"){
        todo.style.display = 'none';
        done.style.display = 'none';
        overdue.style.display = 'none';
        archived.style.display = 'none';
    }
    else if (btn == "overdue"){
        progress.style.display = 'none';
        done.style.display = 'none';
        todo.style.display = 'none';
        archived.style.display = 'none';
    }
    else if (btn == "archived"){
        progress.style.display = 'none';
        done.style.display = 'none';
        todo.style.display = 'none';
        overdue.style.display = 'none';
    }
    else{
    console.log("smth else is clicked")
    }

}

