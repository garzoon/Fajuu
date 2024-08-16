
function openModal(name, type, id) {
    fetch(`/${type}/${id}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('modal-title').innerText = name;
            document.getElementById('modal-body').innerHTML = generateModalContent(data);
            document.getElementById('infoModal').style.display = 'block';
        });
}

function generateModalContent(data) {
    let content = '<ul>';
    for (let key in data) {
        content += `<li><strong>${key}:</strong> ${data[key]}</li> <br>`;
    }
    content += '</ul>';
    return content;
}

document.querySelector('.close').onclick = function() {
    document.getElementById('infoModal').style.display = 'none';
}
