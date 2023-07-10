import {combineReducers} from "redux"

import authReducer from "./auth"
import cleaningsReducer from "./cleanings"
import offersReducer from "./offers"
import uiReducer from "./ui"

const rootReducer = combineReducers({
    auth: authReducer,
    cleanings: cleaningsReducer,
    offers: offersReducer,
    ui: uiReducer,
})

export default rootReducer
