document.getElementById('edit-bio-link').addEventListener('click', function(event) {
  event.preventDefault(); // Prevent the default link behavior
  
  const newBio = prompt('Change your bio here');

  if (newBio) {
    // Populate the hidden input field with the bio value
    document.getElementById("bio-input").value = newBio;

    document.getElementById("bio-form").submit();

      // // Send the POST request to the Flask endpoint
      // fetch('/api/update-bio', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/x-www-form-urlencoded',
      //   },
      //   body: 'bio=' + encodeURIComponent(newBio),
      // })
      // .then((res) => {
      //   // Handle the response from the Flask endpoint
      //   if (res.ok) {
      //     console.log('bio updated successfully');
      //   } else {
      //     console.log('error updating bio');
      //   }
      // })
      // .catch((err) => {
      //   console.log('Error:', err);
      // });
    }
  
});