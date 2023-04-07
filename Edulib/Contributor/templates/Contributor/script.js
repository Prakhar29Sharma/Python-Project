// Code for dynamic dropdown

// Get the subject dropdown and topic dropdown
const subjectDropdown = document.getElementById('subject');
const topicDropdown = document.getElementById('topic');

// Define the options for each topic dropdown
const mathTopics = ['Algebra', 'Geometry', 'Calculus'];
const scienceTopics = ['Biology', 'Chemistry', 'Physics'];
const historyTopics = ['Ancient History', 'Medieval History', 'Modern History'];

// Add an event listener to the subject dropdown
subjectDropdown.addEventListener('change', function() {
  // Get the selected subject
  const selectedSubject = subjectDropdown.value;

  // Clear the topic dropdown
  topicDropdown.innerHTML = '';

  // Populate the topic dropdown based on the selected subject
  if (selectedSubject === 'math') {
    for (let i = 0; i < mathTopics.length; i++) {
      const option = document.createElement('option');
      option.text = mathTopics[i];
      option.value = mathTopics[i];
      topicDropdown.add(option);
    }
  } else if (selectedSubject === 'science') {
    for (let i = 0; i < scienceTopics.length; i++) {
      const option = document.createElement('option');
      option.text = scienceTopics[i];
      option.value = scienceTopics[i];
      topicDropdown.add(option);
    }
  } else if (selectedSubject === 'history') {
    for (let i = 0; i < historyTopics.length; i++) {
      const option = document.createElement('option');
      option.text = historyTopics[i];
      option.value = historyTopics[i];
      topicDropdown.add(option);
    }
  }
});
