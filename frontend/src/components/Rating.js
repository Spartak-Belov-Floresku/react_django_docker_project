
export default function Rating({value, text, color}) {

    let ratingStars = [];

    const starsReview = (idx, arr) => {

      if(idx < 5){
        arr.push(
            <i key={idx} style={{ color }} className={
              value >= idx + 1
                ? 'fas fa-star'
                  : value >= idx + .5
                      ? 'fas fa-star-half-alt'
                      : 'far fa-star'
            }></i>
          );
        idx++;
        starsReview(idx, arr);
      }

      return;
      
    }

    starsReview(0, ratingStars);

  return (
    <div className='rating'>
      <span>{ratingStars}</span> <span>{text && text}</span>
    </div>
  )
}