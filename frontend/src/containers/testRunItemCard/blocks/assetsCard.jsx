import React, {useEffect, useRef, useState} from 'react';
import {
  Box, Card, CardActionArea, CardContent, CardMedia, Dialog, DialogContent, DialogTitle, Paper
} from "@mui/material";
import VideoThumbnail from "react-video-thumbnail";
import CircularProgress from "@mui/material/CircularProgress";
import PlayArrow from "@mui/icons-material/PlayArrow";
import Typography from "@mui/material/Typography";
import {LocalLoading} from "components/Loading/LocalLoading";


const AssetPromise = ({text}) => {
  return (<Box
    sx={{height: '140px', display: 'flex', flexDirection: 'column', justifyContent: 'space-around', padding: '1rem'}}
  >
    <Box sx={{width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
      <CircularProgress/>
    </Box>
    <Typography variant={'subtitle2'}>
      {text}
    </Typography>
  </Box>)
}


const VideoCardPicture = ({url}) => {
  const [videoThumbnail, setVideoThumbnail] = useState("")

  if (!url) return <AssetPromise text={"Video recording will be available shortly. Try to reload page in a minute."}/>

  if (videoThumbnail) {
    return (<Box sx={{position: 'relative'}}>
      <CardMedia
        component="img"
        alt="Contemplative Reptile"
        height="140"
        image={videoThumbnail}
        title="Contemplative Reptile"
      />
      <PlayArrow
        sx={{position: 'absolute', top: '50%', left: '50%', transform: "translate(-50%, -50%)", fontSize: '72px'}}/>
    </Box>)
  } else {
    return (<>
      <Box
        sx={{width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', height: '140px'}}
      >
        <CircularProgress/>
      </Box>
      <Box sx={{display: 'none'}}>
        <VideoThumbnail
          renderThumbnail={false}
          videoUrl={url}
          snapshotAtTime={0}
          thumbnailHandler={(thumbnail) => setVideoThumbnail(thumbnail)}
        />
      </Box>
    </>)
  }
}


const ImageCardPicture = ({url}) => {

  if (!url) return <AssetPromise text={"Image will be available shortly. Try to reload page in a minute."}/>

  return (<CardMedia
    component="img"
    alt="Contemplative Reptile"
    height="140"
    image={url}
    title="Contemplative Reptile"
  />)
}


const TextCardPicture = ({url}) => {

  if (!url) return <AssetPromise text={"Text will be available shortly. Try to reload page in a minute."}/>

  const image_id = useRef({});
  if (!image_id.current[url]) {
    image_id.current[url] = Math.floor(Math.random() * 8) + 1
  }

  return (<CardMedia
    component="img"
    height="140"
    image={`/assets/images/text/${image_id.current[url]}.jpg`}
  />)
}


const VideoCardContent = ({title, url}) => {
  return (<CardMedia
    sx={{
      '& .MuiCardMedia-media': {
        height: '100%'
      }
    }}
    component='video'
    src={url}
    controls
    alt={title}
    title={title}
  />)
}


const ImageCardContent = ({title, url}) => {
  return (<img style={{height: "100%", objectFit: "contain"}} src={url} alt={title}></img>)
}


const TextCardContent = ({url}) => {

  const [text, setText] = React.useState("");

  useEffect(() => {
    fetch(url)
      .then((response) => response.text())
      .then((textContent) => {
        setText(textContent);
      });
  }, [url])

  if (!text) return <LocalLoading/>

  return (<Paper sx={{width: '100%', whiteSpace: 'pre-wrap', wordBreak: 'break-word'}}>
    {text}
  </Paper>)
}

export const AssetCardMemo = ({type, title, url}) => {
  const [open, setOpen] = useState(false)

  const handleOpen = () => {
    if (url) {
      setOpen(true)
    }
  }

  return (<>
    <Card
      onClick={handleOpen}
      elevation={3}
      sx={{textAlign: 'center', position: 'relative'}}
    >
      <CardActionArea>
        {type === "video" && <VideoCardPicture url={url}/>}
        {type === "image" && <ImageCardPicture url={url}/>}
        {type === "text" && <TextCardPicture url={url}/>}
        <CardContent>
          <Box component="h5" sx={{margin: 0}}>{title}</Box>
        </CardContent>
      </CardActionArea>
    </Card>
    <Dialog
      open={open}
      sx={{
        '& .MuiDialog-paper': {height: '100%'}
      }}
      onClose={() => setOpen(false)}
      maxWidth='lg'
      fullWidth={true}
    >
      <DialogTitle sx={{textAlign: 'center'}}>{title}</DialogTitle>
      <DialogContent sx={{display: 'flex', flexDirection: 'column'}}>
        {type === "video" && <VideoCardContent title={title} url={url}/>}
        {type === "image" && <ImageCardContent title={title} url={url}/>}
        {type === "text" && <TextCardContent url={url}/>}
      </DialogContent>
    </Dialog>
  </>);
};

export const AssetCard = React.memo(AssetCardMemo);
