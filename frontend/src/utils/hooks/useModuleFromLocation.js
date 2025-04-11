import {useLocation} from "react-router-dom";

export const projectModules = ["auto", "script_runner", "load_test"]

export const useModuleFromLocation = () => {
      const {pathname} = useLocation();
      return projectModules.filter(module => pathname.toLowerCase().includes(module.toLowerCase()))[0]
}
