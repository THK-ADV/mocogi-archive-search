if (performance.navigation.type == performance.navigation.TYPE_RELOAD) {
    document.getElementById('department').value = '0';
    document.getElementById('y1').value = '2024';
    document.getElementById('y2').value = '2024';
    document.getElementById('l-y1').innerText = '2024';
    document.getElementById('l-y2').innerText = '2024';
}
const option0 = {
    "id": '0',
    "title": 'Select Course'
};
addOption(option0)
var dep= '0'
var semester='Winter'
function getData() {
    const courseId = document.getElementById('course').value;
    const y1 = document.getElementById('y1').value;
    const y2 = document.getElementById('y2').value;
console.log('semester: '+semester)

    // JavaScript code to fetch data from Django REST API
    const data1 = {
        courseId: courseId,
        year: y1,
        semester: semester,
    };
    const data2 = {
        courseId: courseId,
        year: y2,
        semester: semester,
    };
    // The Django API endpoint URL
    const apiUrl = `/data/`;

    // Use fetch to get data from the Django API
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data1),
    })
        .then(response => response.text())  // Parse the JSON response
        .then(data => {

            console.log(data)
            document.getElementById('d-y1').innerText = data;

        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
      fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data2),
    })
        .then(response => response.text())  // Parse the JSON response
        .then(data => {

            console.log(data)
            document.getElementById('d-y2').innerText = data;

        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });



}

function loadCourses() {
    dep= document.getElementById('department').value;
    console.log((dep))
    if(dep==='0') {

        return;
    }

    document.getElementById('course').innerHTML = '';
    addOption(option0)
    clear()
    // JavaScript code to fetch data from Django REST API
    const data = {
        dep,
        semester
    };

    // The Django API endpoint URL
    const apiUrl = `/courses/`;

    // Use fetch to get data from the Django API
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())  // Parse the JSON response
        .then(data => {

            for (const d in data) {
                addOption(data[d])
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });




}

function changeSemester(s){
    semester=s;
    loadCourses();
}
function addOption(op) {
    const selectElement = document.getElementById('course');

    // Create a new <option> element
    const newOption = document.createElement('option');
    newOption.value = op.id;  // Set value
    newOption.textContent = op.title;  // Set text

    // Append the new option to the select element
    selectElement.appendChild(newOption);

}

// Function to remove the last option
function clear() {
    document.getElementById('course').value = '0';
    document.getElementById('y1').value = '0';
    document.getElementById('y2').value = '0';
    document.getElementById('l-y1').value = '0';
    document.getElementById('l-y2').value = '0';
    document.getElementById('d-y1').value = '0';
    document.getElementById('d-y2').value = '0';

    // Check if there are any options to remove

}

function on_y1_change() {
    document.getElementById('l-y1').innerText = document.getElementById('y1').value;
}

function on_y2_change() {
    document.getElementById('l-y2').innerText = document.getElementById('y2').value;
}