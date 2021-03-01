package com.overwhale.colibri_so.frontend.mapper;

import com.overwhale.colibri_so.backend.entity.Snippet;
import com.overwhale.colibri_so.backend.entity.SnippetIntent;
import com.overwhale.colibri_so.frontend.dto.SnippetDto;
import com.overwhale.colibri_so.frontend.dto.SnippetIntentDto;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface SnippetIntentMapper {
  SnippetIntentMapper INSTANCE = Mappers.getMapper(SnippetIntentMapper.class);

  SnippetIntent dtoToEntiy(SnippetIntentDto dto);

  SnippetIntentDto entityToDto(SnippetIntent entity);
}
