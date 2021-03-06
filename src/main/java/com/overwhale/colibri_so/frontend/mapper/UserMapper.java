package com.overwhale.colibri_so.frontend.mapper;

import com.overwhale.colibri_so.backend.entity.User;
import com.overwhale.colibri_so.frontend.dto.UserDto;
import org.mapstruct.Mapper;

@Mapper
public interface UserMapper {
  User dtoToEntiy(UserDto dto);

  UserDto entityToDto(User entity);
}
