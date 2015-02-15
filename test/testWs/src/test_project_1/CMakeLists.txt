###########
## Setup ##
###########

cmake_minimum_required(VERSION 2.8.3)
project(test_project_1)

find_package(catkin_simple REQUIRED)

catkin_simple()

#################
## Executables ##
#################

add_executable({${PROJECT_NAME} 
  src/test.cpp
)

##################
## Installation ##
##################

cs_install()

#############
## Exports ##
#############

cs_export(INCLUDE_DIRS ${catkin_INCLUDE_DIRS})

#############
## Testing ##
#############

