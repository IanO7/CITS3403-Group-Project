/*const pass_profileName = "eye"
const pass_profileImage = "static/download.jpg"
var pass_post = [{resturant:"Bubble Tea", price:"$10", rating: "5", review:"very good, nice atmosphere", image:"static/food.jpg"}, {resturant:"coffe and cake", price:"$100", rating: "1", review:"very bad, terrible atmosphere"}, {resturant:"Bubble Tea", price:"$10", rating: "5", review:"very good, nice atmosphere", image:"static/food.jpg"}] 
*/ 


createProfilePage()
pullPosts()

function createProfilePage(){
    const profileHeader = document.getElementById("profileHeader");
    const profileSub = document.getElementById("profileSub"); 

    let profileImage = document.createElement("img");
    profileImage.setAttribute("src", pass_profileImage); 
    profileImage.classList.add("profileImage")

    let profileName = document.createElement("h1");
    profileName.innerHTML = user; 

    let addPost = document.createElement("button"); 
    addPost.textContent = "+";
    addPost.classList.add("addPost"); 
    addPost.setAttribute("onclick", "location.href='/new_post'");  

    
    profileHeader.appendChild(profileImage);
    profileSub.appendChild(profileName);
    profileSub.appendChild(addPost); 
}

function pullPosts() {
    const profileContent = document.getElementById("content");

    for (let i = 0; i < pass_post.length; i++) {
        let postData = pass_post[i];

        let newPost = document.createElement("div");
        newPost.classList.add("post");

        newPost.innerHTML = `
            <div class="p-3" >
                <h3>${postData.resturant}</h3>
                <p>Price: ${postData.price}</p>
                <p>Rating: ${postData.rating}</p>
                <p>Review: ${postData.review}</p>
            </div> 
            ${postData.image ? `<img src="${postData.image}" class="postImage">` : ""}
        `;

        profileContent.appendChild(newPost);
    }


}
