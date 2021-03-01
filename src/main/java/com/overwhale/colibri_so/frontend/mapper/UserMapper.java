package com.overwhale.colibri_so.frontend.mapper;

import com.overwhale.colibri_so.backend.entity.Intent;
import com.overwhale.colibri_so.backend.entity.User;
import com.overwhale.colibri_so.frontend.dto.IntentDto;
import com.overwhale.colibri_so.frontend.dto.UserDto;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface UserMapper {
  UserMapper INSTANCE = Mappers.getMapper(UserMapper.class);

  User dtoToEntiy(UserDto dto);

  UserDto entityToDto(User entity);
}
