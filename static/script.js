document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('prediction-form').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the form from submitting the traditional way
        const region = document.getElementById('region').value;
        const temp = parseFloat(document.getElementById('temp').value);
        const rh = parseFloat(document.getElementById('rh').value);
        const ws = parseFloat(document.getElementById('ws').value);
        const rain = parseFloat(document.getElementById('rain').value);
        const ffmc = parseFloat(document.getElementById('ffmc').value);
        const dmc = parseFloat(document.getElementById('dmc').value);
        const isi = parseFloat(document.getElementById('isi').value);
        const fireClass = document.getElementById('class').value;

        // Create a data object
        const dataObject = {
            region: region,
            Temperature: temp,
            RH: rh,
            Ws: ws,
            Rain: rain,
            FFMC: ffmc,
            DMC: dmc,
            ISI: isi,
            Classes: fireClass
        };

        // Log the data object to ensure it's correctly formatted
        console.log('Form data object:', dataObject);


        // Log the data object to ensure it's correctly formatted
        console.log('Form data object:', dataObject);

        // Create an XMLHttpRequest object
        const xhr = new XMLHttpRequest();

        // Configure it: POST-request for the URL /predict
        xhr.open('POST', '/predict', true);

        // Set the Content-Type header to application/json
        xhr.setRequestHeader('Content-Type', 'application/json');

        // Set up the callback function to handle the response
        xhr.onload = function() {
            if (xhr.status >= 200 && xhr.status < 300) {
                // Successful response
                const response = JSON.parse(xhr.responseText);
                console.log('Server response:', response);
                // Display the prediction on the webpage
                // Find the card element
                const cardElement = document.querySelector('.card');

                // Remove existing footer if it exists
                const existingFooter = cardElement.querySelector('.card-footer');
                if (existingFooter) {
                    cardElement.removeChild(existingFooter);
                }

                // Create a new footer element to display the prediction
                const footerElement = document.createElement('div');
                footerElement.className = 'card-footer text-body-secondary';  // Use appropriate class for styling
                footerElement.innerText = `Prediction: ${response.prediction}`;

                // Append the new footer element to the card
                cardElement.appendChild(footerElement);
            } else {
                // Handle errors
                console.error('Error:', xhr.statusText);
            }
        };

        // Send the form data as JSON
        xhr.send(JSON.stringify(dataObject));
    });
});
