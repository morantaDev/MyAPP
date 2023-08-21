const suggestButton = document.getElementById('suggestButton');
const cuisineInput = document.getElementById('cuisine');
const ingredientsInput = document.getElementById('ingredients');
const suggestionsDiv = document.getElementById('suggestions');



suggestButton.addEventListener('click', () => {
    const cuisine = cuisineInput.value;
    const ingredients = ingredientsInput.value.split(',').map(item => item.trim());


    // Faire une requête AJAX vers le serveur
    fetch('http://127.0.0.1:8000/get_suggestions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cuisine, ingredients })
    })
    .then(response => response.json())
    .then(data => {
        const suggestions = data.suggestions;
        suggestionsDiv.innerHTML = suggestions.map(recipe => `<p>${recipe}</p>`).join('');
    })
    .catch(error => {
        console.error('Erreur de requête AJAX :', error);
    });
});
// });
    
    