var searchBar = getFirstElementByName("searchBar");

var hiddenTeamsSpan = getFirstElementByName("hiddenSpan");

var seeTeams = getFirstElementByName("seeTeams");

var teamsArray = document.getElementById("mainContainer").getElementsByClassName("media");




function showHiddenTeams() {
    if (searchBar.value != "") {
        hiddenTeamsSpan.style.display = 'block';
        seeTeams.style.display = 'none';
        for (i = 0; i < teamsArray.length; i++) {
            if(teamsArray[i].children[1].children[0].innerHTML.toLowerCase().includes(searchBar.value.toLowerCase()) || teamsArray[i].children[1].children[2].innerHTML.toLowerCase().includes(searchBar.value.toLowerCase())){
                teamsArray[i].style.display = 'block';
            }
            else{
                teamsArray[i].style.display = 'none';
            }
        }
    }
    else {
        hiddenTeamsSpan.style.display = 'none';
        seeTeams.style.display = 'block';
        for (i = 0; i < teamsArray.length; i++) {
            teamsArray[i].style.display = 'block';
        }
    }
}

function getFirstElementByName(element_name) {
    var elements = document.getElementsByName(element_name);
    if (elements.length) {
        return elements[0];
    } else {
        return undefined;
    }
}