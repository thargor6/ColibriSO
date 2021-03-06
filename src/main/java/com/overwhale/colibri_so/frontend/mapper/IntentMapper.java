package com.overwhale.colibri_so.frontend.mapper;

import com.overwhale.colibri_so.backend.entity.Intent;
import com.overwhale.colibri_so.frontend.dto.IntentDto;
import org.mapstruct.Mapper;

@Mapper
public interface IntentMapper {
  Intent dtoToEntiy(IntentDto dto);

  IntentDto entityToDto(Intent entity);
}
