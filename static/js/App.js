//selectors
const preferences = document.querySelector('.preferences');
const createPlanBtn = document.querySelector('.create-trip-btn')
const checkinDate = document.querySelector('.form-control-checkin')
const checkoutDate = document.querySelector('.form-control-checkout')

//event listeners
createPlanBtn.addEventListener('click', (event)=>{
    //prevent form from submitting
    //event.preventDefault()
})

//preference list
const preferenceList = ["Adult", "Amusements", 
"Architecture", 
"Cultural", 
"Historical", 
"Industrial Facilliites", 
"Natural", 
"Other", 
"Religion", 
"Sport",
"Tourist Facilities"]

//functions

//Create preference
function createPreferences(preference){
    const checkbox = document.createElement('input')
    checkbox.type = 'checkbox'
    checkbox.value=preference
    checkbox.id = 'flexCheckDefault'
    checkbox.classList.add('form-check-input');

    const label = document.createElement('label')
    label.htmlFor = 'flexCheckDefault'
    label.classList.add('form-check-label');
    label.innerText = preference

    const container = document.createElement('form-check');
    container.appendChild(checkbox);
    container.append(label);

    preferences.appendChild(container)
}

//Get selected preferences
function getCheckedPreferences(){
    var array = []
    var prerefenceList = []
    var checkboxes = document.querySelectorAll('input[type=checkbox]:checked')
    for (var i = 0; i < checkboxes.length; i++) {
    array.push(checkboxes[i].value)
    }
    array.forEach(preference => {
        preferenceList.push(preference)
    })
    return preferenceList
}

//Loop and add prerefence 
preferenceList.forEach(preference => {
    createPreferences(preference);
})