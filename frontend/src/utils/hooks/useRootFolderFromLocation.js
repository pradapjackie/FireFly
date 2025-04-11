import {useLocation} from "react-router-dom";

export const useRootFolderFromLocation = () => {
      const {pathname} = useLocation();
      return pathname.split("/")[2]
}
