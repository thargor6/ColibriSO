package com.overwhale.colibri_so.frontend.mapper;

import com.overwhale.colibri_so.backend.entity.UserDetail;
import com.overwhale.colibri_so.frontend.dto.UserDetailDto;
import org.mapstruct.Mapper;

@Mapper
public interface UserDetailMapper {
  UserDetail dtoToEntiy(UserDetailDto dto);

  UserDetailDto entityToDto(UserDetail entity);
}
