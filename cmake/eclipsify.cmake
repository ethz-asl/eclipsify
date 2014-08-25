
FUNCTION(eclipsify)
  # Emit an eclipse project in devel/share/package/eclipse
  #get_cmake_property(_variableNames VARIABLES)
  #foreach (_variableName ${_variableNames})
  #  message(STATUS "${_variableName}=${${_variableName}}")
  #endforeach()

  # There is no way to get the gtest target binaries

  # CATKIN_DEVEL_PREFIX=/Users/ptf/Work/ethz/code/aslam/devel
  # CMAKE_BINARY_DIR=/Users/ptf/Work/ethz/code/aslam/build/aslam_cv
  # CATKIN_PACKAGE_SHARE_DESTINATION=share/aslam_cv
  # eclipsify_DEVEL_PREFIX=/Users/ptf/Work/ethz/code/aslam/devel
  # CMAKE_RUNTIME_OUTPUT_DIRECTORY=/Users/ptf/Work/ethz/code/aslam/devel/lib/aslam_cv

  set(share_directory ${CATKIN_DEVEL_PREFIX}/${CATKIN_PACKAGE_SHARE_DESTINATION})
  set(eclipse_directory ${CATKIN_DEVEL_PREFIX}/${CATKIN_PACKAGE_SHARE_DESTINATION}/eclipse)
  
  file(MAKE_DIRECTORY ${share_directory})
  file(MAKE_DIRECTORY ${eclipse_directory})

  execute_process(
    COMMAND
    eclipsify-gen-project
    "${CMAKE_PROJECT_NAME}" 
    "${CMAKE_SOURCE_DIR}"
    "${eclipse_directory}" 
    "${CMAKE_BINARY_DIR}"
    #"${CMAKE_RUNTIME_OUTPUT_DIRECTORY}"
    WORKING_DIRECTORY ${eclipse_directory})
ENDFUNCTION()

