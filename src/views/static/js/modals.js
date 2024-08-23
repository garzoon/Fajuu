
function view_modal(title) {

    const modal = document.getElementById('infoModal');
    const span = document.getElementsByClassName('close')[0];


    document.getElementById('modal-title').innerText = title
    modal.style.display = 'block'

    
    span.onclick = function() {
        modal.style.display = 'none'
    }
    window.onclick = function(event) {
        if(event.target == modal) {
            modal.style.display = 'none'
        }
    } 
}


function delete_modal(redirect, id) {

    const modal = document.getElementById('delete_modal');
    const span = document.getElementsByClassName('delete_modal_close')[0];
    const close_modal = document.getElementById('close_button')

    modal.style.display = 'block'
    document.getElementById('delete_form').action = `${redirect}/${id}`;

    span.onclick = function() {
        modal.style.display = 'none'
    }
    close_modal.onclick = function() {
        modal.style.display = 'none'    
    }
    window.onclick = function(event) {
        if(event.target == modal) {
            modal.style.display = 'none'
        }
    } 
}


