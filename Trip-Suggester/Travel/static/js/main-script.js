


const preloader = document.querySelector("[data-prelaoder]");
window.addEventListener("load", () => {
preloader.classList.add("remove")
});





const addEventOnElements = function(elements, eventType, callback) {
  console.log("Elements:", elements); // Check array contents
    for (let i=0, len=elements.length; i<len; i++) {
      console.log("Adding event listener to element:", elements[i]);
        elements[i].addEventListener(eventType,callback)

    }
}



const navbar= document.querySelector("[data-navbar]")
const navTogglers= document.querySelectorAll("[data-nav-toggler]")
const overlay= document.querySelector("[data-overlay]")



const toggleNav = function() {
    navbar.classList.toggle("active")
    overlay.classList.toggle("active")
    document.body.classList.toggle("nav-active")
}


addEventOnElements(navTogglers, "click" , toggleNav);{

};





const header = document.querySelector("[data-header]");

window.addEventListener("scroll", function(){
    header.classList[window.scrollY > 100 ? "add" : "remove"] ("active");
});





















const planTripButton = document.querySelector("[data-entry]"); // Select the button
const formContainer = document.querySelector("[data-form]"); // Select the form container




planTripButton.addEventListener('click', () => {
formContainer.classList.toggle("hidden"); // Show the form

});








var el = document.querySelector('[data-entry]');

el.addEventListener('click' , e=> console.log('Click') );