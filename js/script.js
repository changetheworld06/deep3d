// Bouton J'aime
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.like-btn').forEach(button => {
      const projet = button.dataset.projet;
      const compteur = button.querySelector('.like-count');
      
      // Charger le nombre de likes depuis le localStorage
      const likes = localStorage.getItem(`likes-${projet}`) || 0;
      compteur.textContent = likes;
  
      button.addEventListener('click', () => {
        let newLikes = parseInt(likes) + 1;
        localStorage.setItem(`likes-${projet}`, newLikes);
        compteur.textContent = newLikes;
      });
    });
  
    // Bouton de partage
    document.querySelectorAll('.share-btn').forEach(button => {
      button.addEventListener('click', () => {
        const url = button.dataset.url;
        if (navigator.share) {
          navigator.share({
            title: document.title,
            url: url
          }).catch((err) => console.log('Erreur de partage :', err));
        } else {
          navigator.clipboard.writeText(url);
          alert("Lien copié !");
        }
      });
    });
  });