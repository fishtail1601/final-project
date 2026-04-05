/**
 * Toggles the display of an individual team member's bio
 * @param {string} bioId - The ID of the bio section to show or hide
 */
function toggleBio(bioId) {
    const bio = document.getElementById(bioId);
    // Toggle between showing and hiding the bio section
    if (bio.style.display === "none" || bio.style.display === "") {
        bio.style.display = "block";
    } else {
        bio.style.display = "none";
    }
}

/**
 * Shows the specified section ('bios' or 'vision') and hides the other
 * @param {string} sectionId - The ID of the section to display
 */
function showSection(sectionId) {
    const biosSection = document.getElementById("bios");
    const visionSection = document.getElementById("vision");
    const moodboardSection = document.getElementById("moodboard");

    // Hide everything first
    biosSection.style.display = "none";
    visionSection.style.display = "none";
    moodboardSection.style.display = "none";

    // Show the selected section
    if (sectionId === "bios") {
        biosSection.style.display = "flex";
    } else if (sectionId === "vision") {
        visionSection.style.display = "block";
    } else if (sectionId === "moodboard") {
        moodboardSection.style.display = "block";
    }
}
