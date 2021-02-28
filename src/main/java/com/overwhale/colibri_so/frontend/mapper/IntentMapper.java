package com.overwhale.colibri_so.frontend.mapper;

import com.overwhale.colibri_so.backend.entity.Intent;
import com.overwhale.colibri_so.frontend.dto.IntentDto;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface IntentMapper {
    IntentMapper INSTANCE = Mappers.getMapper( IntentMapper.class );
    Intent dtoToEntiy(IntentDto dto);
    IntentDto entityToDto(Intent entity);
}
