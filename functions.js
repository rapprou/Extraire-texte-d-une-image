// functions js 

document.getElementById('upload-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    let fileInput = document.getElementById('image-file');
    if (fileInput.files.length === 0) {
        alert('Veuillez sélectionner une image.');
        return;
    }

    let formData = new FormData();
    formData.append('image', fileInput.files[0]);

    try {
        let response = await fetch('http://127.0.0.1:5000/extract-text', {
            method: 'POST',
            body: formData
        });
        // Vérifier la réponse du serveur
        if (!response.ok) {
            document.getElementById('result').innerText = 'Erreur du serveur : ' + response.statusText;
            return;
        }

        // Analyser la réponse JSON
        let data = await response.json();
        if (data.error) {
            document.getElementById('result').innerText = 'Erreur: ' + data.error;
        } else {
            document.getElementById('result').innerText = data.text || 'Aucun texte trouvé.';
        }

    } catch (error) {
        console.error('Une erreur est survenue lors de la soumission:', error);
        document.getElementById('result').innerText = 'Erreur: ' + error.message;
    }

});
