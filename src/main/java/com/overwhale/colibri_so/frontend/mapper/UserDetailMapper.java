package com.overwhale.colibri_so.frontend.mapper;

import com.overwhale.colibri_so.backend.entity.User;
import com.overwhale.colibri_so.backend.entity.UserDetail;
import com.overwhale.colibri_so.frontend.dto.UserDetailDto;
import com.overwhale.colibri_so.frontend.dto.UserDto;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface UserDetailMapper {
  UserDetailMapper INSTANCE = Mappers.getMapper(UserDetailMapper.class);

  UserDetail dtoToEntiy(UserDetailDto dto);

  UserDetailDto entityToDto(UserDetail entity);
}
