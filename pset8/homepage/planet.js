/* Toggle the "More Facts" button on single planet pages */

var moreFactsButton = document.querySelector('#more-facts');
var factsText = document.querySelector('#facts');

moreFactsButton.addEventListener("click", function() {
    factsText.classList.toggle('hidden');
});