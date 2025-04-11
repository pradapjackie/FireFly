import React, {createContext, useContext} from 'react';

const FormContext = createContext(null)
const SetFormContext = createContext(null)

export const FormContextProvider = ({resultConfig, setResultConfig, children}) => {

  return (
    <FormContext.Provider value={resultConfig}>
      <SetFormContext.Provider value={setResultConfig}>
        {children}
      </SetFormContext.Provider>
    </FormContext.Provider>
  )
}

export const useFormContext = () => {
  const formContext = useContext(FormContext)
  const handleFormChange = useContext(SetFormContext)
  return [formContext, handleFormChange]
}
