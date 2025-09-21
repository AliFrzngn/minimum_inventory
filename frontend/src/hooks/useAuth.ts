import { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { RootState, AppDispatch } from '../store/store'
import { getCurrentUser } from '../store/slices/authSlice'

export const useAuth = () => {
  const dispatch = useDispatch<AppDispatch>()
  const { user, token, isLoading, error } = useSelector((state: RootState) => state.auth)

  useEffect(() => {
    if (token && !user) {
      dispatch(getCurrentUser())
    }
  }, [token, user, dispatch])

  const isAuthenticated = !!user && !!token

  return {
    user,
    token,
    isLoading,
    error,
    isAuthenticated,
  }
}
