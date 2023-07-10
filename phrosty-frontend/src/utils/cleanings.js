export const userIsOwnerOfCleaningJob = (cleaning, user) => {
    if (cleaning?.owner?.id === user?.id) return true
    return cleaning?.owner === user?.id;

}
