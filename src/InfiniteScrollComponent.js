import React, { useState, useEffect } from 'react';
import InfiniteScroll from 'react-infinite-scroll-component';
import ImageComponent from './Content Components/ImageComponent';
import TextComponent from './Content Components/TextComponent';
import './styles.css';

import { useFetchText } from './useFetchText'
import { useFetchImages } from './useFetchImages'

function InfiniteScrollComponent() {

  const [items, setItems] = useState([]);
  const { texts } = useFetchText()
  const { images } = useFetchImages()

  
  const refreshItems= () => {
    console.log(items)
    try {
      const newItems = [];
      for (let i = 0; i < 5; i++) {
        const itemType = Math.floor(Math.random() * 1);
        switch (itemType) {
          case 0: // Image
            if (images.length) {
              const randomIndex = Math.floor(Math.random() * images.length);
              const image = images[randomIndex];

              if(image.active = 1){
                newItems.push({
                  type: 'image',
                  file: image.file,
                  subtype: image.subtype,
                  tags: image.tags,
                  votes: image.votes,
                  active: image.active,
                  id:image.id,
                  imageUrl:image.imageUrl
                });
              }

            }
            break;
          case 1: // Text
            if (texts.length) {
              const randomIndex = Math.floor(Math.random() * texts.length);
              const text = texts[randomIndex];
              console.log('te', text)
              newItems.push({
                content: text.content,
                type: text.type, subtype: text.subtype,
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

  return (
    <div>
      <InfiniteScroll
        dataLength={items.length}
        next={refreshItems}
        hasMore={true}
        loader={<h4>Loading...</h4>}
      >
        {items.map((item, index) => (
          <div key={index}>
            {randomComponent(item, index)}
          </div>
        ))}

      </InfiniteScroll>
    </div>
  );
}

export default InfiniteScrollComponent;

