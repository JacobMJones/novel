import React, { useState, useEffect } from 'react';
import InfiniteScroll from 'react-infinite-scroll-component';
import ImageComponent from './Content Components/ImageComponent';
import TextComponent from './Content Components/TextComponent';
import './styles.css';

import { useFetchText } from './useFetchText'
import { useFetchImageData } from './useFetchImageData'

function InfiniteScrollComponent() {

  const [items, setItems] = useState([]);
  const { texts } = useFetchText()
  const { images } = useFetchImageData()
  const [userTags, setUserTags] = useState(['ai'])

  const refreshItems = () => {
    console.log(userTags)
    try {
      const newItems = [];
      const filteredImages = images.filter(image => 
        image.tags.split(',').some(tag => userTags.includes(tag.trim())) && image.active === 1
      );
      
      for (let i = 0; i < 5; i++) {
        const itemType = Math.floor(Math.random() * 1);
        switch (itemType) {
          case 0: // Image
            if (filteredImages.length) {
              const randomIndex = Math.floor(Math.random() * filteredImages.length);
              const image = filteredImages[randomIndex];
              if (image.active === 1) {
                newItems.push({
                  type: 'image',
                  file: image.file,
                  subtype: image.subtype,
                  tags: image.tags,
                  votes: image.votes,
                  active: image.active,
                  id: image.id,
                  imageUrl: image.imageUrl,
                  color: image.color,
                  color_rgb: image.color_rgb
                });
              }

            }
            break;
          case 1: // Text poetry
            const filteredTexts = texts.filter(text => text.subtype === 'rumi' || text.subtype === 'tao');


            if (filteredTexts.length) {
              const randomIndex = Math.floor(Math.random() * filteredTexts.length);
              const text = filteredTexts[randomIndex];
              // Extract the first sentence from the text
              const firstSentence = text.text.split(/(?<=[.!?])\s/)[0];

              newItems.push({
                content: firstSentence,
                type: 'text', text_type: text.type, subtype: text.subtype,
                active: text.active,
                tags: text.tags,
                id: text.id
              });
            }
            break;
        }
      }
      setItems(items => [...items, ...newItems]);
    }
    catch (error) {
      console.error("Error fetching items")
    }
  };

  useEffect(() => {
    refreshItems();
  }, [images, texts]);

  const randomComponent = (item, index) => {
    if (item.active === 1) {
      if (item.type === 'text') {
        return <TextComponent key={`text-${index}`} item={item} />;
      } else {
        return <ImageComponent key={`image-${index}`} item={item} alt="random" />;
      }
    }
  };
  const formatColor = (colorRgb, alpha) => {
    return colorRgb ? `rgba(${colorRgb.replace(/[\(\)]/g, '')}, ${alpha})` : 'rgba(0,0,0, 1)';
  };

  return (
    <div>
      <InfiniteScroll
        dataLength={items.length}
        next={refreshItems}
        hasMore={true}
        loader={<h4>Loading...</h4>}

      >
        {items.map((item, index) => {
          const formattedColor = formatColor(item.color_rgb);
          return (
            <div style={{
              padding: '10vh',
              background: `linear-gradient(to bottom, white, ${formatColor(item.color_rgb, .2)} 30%,  ${formatColor(item.color_rgb, .4)} 50%, ${formatColor(item.color_rgb, .2)} 70%, white)`
            }} key={index}>
              <div key={index}>
                {randomComponent(item, index)}
              </div>
            </div>
          )
        }

        )}

      </InfiniteScroll>
    </div>
  );
}

export default InfiniteScrollComponent;

