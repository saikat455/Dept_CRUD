document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("departmentForm");
    const deptNameInput = document.getElementById("deptName");
    const departmentList = document.getElementById("departmentList");

    // Fetch the department list on page load
    fetchDepartments();

    // Handle form submission
    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent page reload
        const deptName = deptNameInput.value;

        // Send POST request to add department
        const response = await fetch("http://127.0.0.1:8000/departments/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name: deptName }),
        });

        if (response.ok) {
            deptNameInput.value = ""; // Clear input field
            fetchDepartments(); // Refresh the department list
        } else {
            alert("Failed to add department");
        }
    });

    // Function to fetch departments from the API
    async function fetchDepartments() {
        const response = await fetch("http://127.0.0.1:8000/departments/");
        const departments = await response.json();
        departmentList.innerHTML = ""; // Clear existing list

        // Display departments
        departments.forEach(department => {
            const li = document.createElement("li");
            li.innerHTML = `
                ${department.name}
                <div>
                    <button onclick='openUpdateModal(${JSON.stringify(department)})'>Update</button>
                    <button onclick='openDeleteModal(${JSON.stringify(department)})'>Delete</button>
                </div>
            `;
            departmentList.appendChild(li);
        });
    }

    // Open Update Department Modal
    window.openUpdateModal = function(dept) {
        document.getElementById('updateDeptId').value = dept.id;
        document.getElementById('updateDeptName').value = dept.name;
        document.getElementById('updateDepartmentModal').style.display = 'block';
    }

    // Close Update Department Modal
    window.closeUpdateModal = function() {
        document.getElementById('updateDepartmentModal').style.display = 'none';
    }

    // Update Department
    document.getElementById('updateDepartmentForm').addEventListener('submit', async function(event) {
        event.preventDefault();
        const id = document.getElementById('updateDeptId').value;
        const name = document.getElementById('updateDeptName').value;

        const response = await fetch(`http://127.0.0.1:8000/departments/${id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name }),
        });

        if (response.ok) {
            closeUpdateModal();
            fetchDepartments(); // Refresh the department list
        } else {
            alert('Failed to update department');
        }
    });

    // Open Delete Department Modal
    window.openDeleteModal = function(dept) {
        document.getElementById('deleteDeptName').innerText = dept.name;
        document.getElementById('deleteDeptId').value = dept.id; // Store ID for deletion
        document.getElementById('deleteDepartmentModal').style.display = 'block';
    }

    // Close Delete Department Modal
    window.closeDeleteModal = function() {
        document.getElementById('deleteDepartmentModal').style.display = 'none';
    }

    // Confirm Delete Department
    window.confirmDeleteDepartment = async function() {
        const id = document.getElementById('deleteDeptId').value;

        const response = await fetch(`http://127.0.0.1:8000/departments/${id}/`, {
            method: 'DELETE',
        });

        if (response.ok) {
            closeDeleteModal();
            fetchDepartments(); // Refresh the department list
        } else {
            alert('Failed to delete department');
        }
    }
});
