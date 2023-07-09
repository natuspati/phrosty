const initialState = {
    auth: {
        isLoading: false,
        isUpdating: false,
        error: false,
        user: {}
    },
    cleanings: {
        isLoading: false,
        error: null,
        data: {},
        currentCleaningJob: null
    }
}

export default initialState
